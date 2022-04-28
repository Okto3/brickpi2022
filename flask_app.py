from flask import Flask, render_template, session, request, redirect, flash, url_for, jsonify, Response, logging
from interfaces import databaseinterface, camerainterface, soundinterface
import robot #robot is class that extends the brickpi class
import global_vars as GLOBALS #load global variables
import logging, time
from datetime import *

#Creates the Flask Server Object
app = Flask(__name__); app.debug = True
SECRET_KEY = 'my random key can be anything' #this is used for encrypting sessions
app.config.from_object(__name__) #Set app configuration using above SETTINGS
logging.basicConfig(filename='logs/flask.log', level=logging.INFO)
GLOBALS.DATABASE = databaseinterface.DatabaseInterface('databases/RobotDatabase.db', app.logger)

Colour = ""

#Log messages
def log(message):
    app.logger.info(message)
    return

#create a login page
@app.route('/', methods=['GET','POST'])
def login():
    if 'userid' in session:
        return redirect('/dashboard')
    message = ""
    if request.method == "POST":
        email = request.form.get("email")
        userdetails = GLOBALS.DATABASE.ViewQuery("SELECT * FROM users WHERE email = ?", (email,))
        log(userdetails)
        if userdetails:
            user = userdetails[0] #get first row in results
            if user['password'] == request.form.get("password"):
                session['userid'] = user['userid']
                #session['permission'] = user['permission']
                session['name'] = user['name']
                return redirect('/dashboard')
            else:
                message = "Login Unsuccessful"
        else:
            message = "Login Unsuccessful"
    return render_template('login.html', data = message)    

# Load the ROBOT
@app.route('/robotload', methods=['GET','POST'])
def robotload():
    sensordict = None
    if not GLOBALS.CAMERA:
        log("LOADING CAMERA")
        try:
            GLOBALS.CAMERA = camerainterface.CameraInterface()
        except Exception as error:
            log("FLASK APP: CAMERA NOT WORKING")
            GLOBALS.CAMERA = None
        if GLOBALS.CAMERA:
            GLOBALS.CAMERA.start()
    if not GLOBALS.ROBOT: 
        log("FLASK APP: LOADING THE ROBOT")
        GLOBALS.ROBOT = robot.Robot(10, app.logger)
        GLOBALS.ROBOT.configure_sensors() #defaults have been provided but you can 
        GLOBALS.ROBOT.reconfig_IMU()
    if not GLOBALS.SOUND and GLOBALS.ROBOT.BP != "Cheese.":
        log("FLASK APP: LOADING THE SOUND")
        GLOBALS.SOUND = soundinterface.SoundInterface()
        GLOBALS.SOUND.say("I am ready")
    if GLOBALS.ROBOT.BP != "Cheese.":
        sensordict = GLOBALS.ROBOT.get_all_sensors()
    return jsonify(sensordict)

# ---------------------------------------------------------------------------------------
# Dashboard
@app.route('/dashboard', methods=['GET','POST'])
def robotdashboard():
    if not 'userid' in session:
        return redirect('/')
    enabled = int(GLOBALS.ROBOT != None)
    return render_template('dashboard.html', robot_enabled = enabled, Colour = Colour )

#Used for reconfiguring IMU
@app.route('/reconfig_IMU', methods=['GET','POST'])
def reconfig_IMU():
    if GLOBALS.ROBOT:
        GLOBALS.ROBOT.reconfig_IMU()
        sensorconfig = GLOBALS.ROBOT.get_all_sensors()
        return jsonify(sensorconfig)
    return jsonify({'message':'ROBOT not loaded'})

#calibrates the compass but takes about 10 seconds, rotate in a small 360 degrees rotation
@app.route('/compass', methods=['GET','POST'])
def compass():
    data = {}
    if GLOBALS.ROBOT:
        data['message'] = GLOBALS.ROBOT.calibrate_imu(10)
    return jsonify(data)

@app.route('/sensors', methods=['GET','POST'])
def sensors():
    data = {}
    if GLOBALS.ROBOT:
        data = GLOBALS.ROBOT.get_all_sensors()
    return jsonify(data)

# YOUR FLASK CODE------------------------------------------------------------------------
@app.route('/shoot', methods=['GET','POST'])
def shoot():
    data = {}
    if GLOBALS.SOUND:
        GLOBALS.SOUND.say("You will be destroyed")
    if GLOBALS.ROBOT:
        GLOBALS.ROBOT.spin_medium_motor(2000)
    return jsonify(data)

@app.route('/moveforward', methods=['GET','POST'])
def moveforward():
    data = {}
    if GLOBALS.ROBOT:
        data['elapsedtime'] = GLOBALS.ROBOT.move_power(20,1)
        data['heading'] = GLOBALS.ROBOT.get_compass_IMU()
    return jsonify(data)

@app.route('/movebackwards', methods=['GET','POST'])
def movebackwards():
    data = {}
    if GLOBALS.ROBOT:
        data['elapsedtime'] = GLOBALS.ROBOT.move_power(-20,0)
        data['heading'] = GLOBALS.ROBOT.get_compass_IMU()
    return jsonify(data)

@app.route('/turnLeft', methods=['GET','POST'])
def turnLeft():
    data = {}
    if GLOBALS.ROBOT:
        GLOBALS.ROBOT.rotate_power_degrees_IMU(20,20)
    return jsonify(data)

@app.route('/turnRight', methods=['GET','POST'])
def turnRight():
    data = {}
    if GLOBALS.ROBOT:
        GLOBALS.ROBOT.rotate_power_degrees_IMU(20,-20)
    return jsonify(data)

@app.route('/stop', methods=['GET','POST'])
def stop():
    data = {}
    if GLOBALS.ROBOT:
        GLOBALS.ROBOT.stop_all()
    return jsonify(data)

@app.route('/searchMaze', methods=['GET','POST'])
def searchMaze():
    data = {}
    if GLOBALS.ROBOT:
        GLOBALS.ROBOT.automatedSearch()
    return jsonify(data)

@app.route('/autonomouseSearch', methods=['GET','POST'])
def autonomouseSearch():
    data = None

    return render_template('autonomouseSearch.html')


@app.route('/mission', methods=['GET','POST'])
def mission():
    data = None
    if request.method == "POST":
        userID = session['userid']
        notes = request.form.get('notes')
        location = request.form.get('location')
        startTime = datetime.now()
        log("flask app mission" + str(location) + ",  " + str(notes) + ",  " + str(startTime))
        GLOBALS.DATABASE.ModifyQuery("INSERT INTO mission (startTime, location, notes, endTime,userID,missionMap) VALUES (?,?,?,?,?,?)",(10,"ashgrove","dead",11,1,"none"))
    #get mission id and save in session
    return render_template("mission.html", data=data)

@app.route('/sensorView', methods=['GET','POST'])
def sensorView():
    data=None
    if GLOBALS.ROBOT:
        data = GLOBALS.ROBOT.get_all_sensors()
    else:
        return redirect('/dashboard')
    
    return render_template("sensorView.html", data = data)


# -----------------------------------------------------------------------------------
# CAMERA CODE-----------------------------------------------------------------------
# Continually gets the frame from the pi camera
def videostream():
    """Video streaming generator function."""
    while True:
        if GLOBALS.CAMERA:
            frame = GLOBALS.CAMERA.get_frame()
            if frame:
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
            else:
                return '', 204
        else:
            return '', 204 

#embeds the videofeed by returning a continual stream as above
@app.route('/videofeed', methods=['GET','POST'])
def videofeed():
    if GLOBALS.CAMERA:
        log("FLASK APP: READING CAMERA")
        """Video streaming route. Put this in the src attribute of an img tag."""
        Colour = GLOBALS.CAMERA.get_camera_colour()
        log(Colour)
        return Response(videostream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return '', 204
        
#----------------------------------------------------------------------------
#Shutdown the robot, camera and database
def shutdowneverything():
    log("FLASK APP: SHUTDOWN EVERYTHING")
    if GLOBALS.CAMERA:
        GLOBALS.CAMERA.stop()
    if GLOBALS.ROBOT:
        GLOBALS.ROBOT.safe_exit()
    GLOBALS.CAMERA = None; GLOBALS.ROBOT = None; GLOBALS.SOUND = None
    return

#Ajax handler for shutdown button
@app.route('/robotshutdown', methods=['GET','POST'])
def robotshutdown():
    shutdowneverything()
    return jsonify({'message':'robot shutdown'})

#Shut down the web server if necessary
@app.route('/shutdown', methods=['GET','POST'])
def shutdown():
    shutdowneverything()
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return jsonify({'message':'Shutting Down'})

@app.route('/logout')
def logout():
    shutdowneverything()
    session.clear()
    return redirect('/')

#---------------------------------------------------------------------------
#main method called web server application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True) #runs a local server on port 5000
    