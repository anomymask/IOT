from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

def generate_frames():
    # 웹캠을 사용하거나 영상 파일을 열 수 있습니다.
    camera = cv2.VideoCapture(0)  # 0은 기본 웹캠을 의미합니다.

    while True:
        # 프레임을 읽어들입니다.
        success, frame = camera.read()
        if not success:
            break
        else:
            # 프레임을 JPEG 형식으로 인코딩합니다.
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # 클라이언트에게 스트림을 보내는 부분입니다.
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
