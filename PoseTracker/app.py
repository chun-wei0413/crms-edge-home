import cv2
import mediapipe as mp
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from utils.minio import MinioClientManager
from utils.env import *
import os
from utils.extract_frame import *

mp_drawing = mp.solutions.drawing_utils  # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_holistic = mp.solutions.holistic  # mediapipe 全身偵測方法

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

minioClient = MinioClientManager(
    get_env_minio_host(),
    get_env_minio_user(),
    get_env_minio_password(),
    secure=False
)

thumbnail_file_extension = "-thumbnail.jpg"


def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("Cannot open video")
        return False

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (520, 300))

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                break
            img = cv2.resize(img, (520, 300))
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 將 BGR 轉換成 RGB
            results = holistic.process(img2)  # 開始偵測全身

            # 面部偵測，繪製臉部網格
            if results.face_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    results.face_landmarks,
                    mp_holistic.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_contours_style())

            # 身體偵測，繪製身體骨架
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    results.pose_landmarks,
                    mp_holistic.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles
                    .get_default_pose_landmarks_style())

            out.write(img)

    cap.release()
    out.release()
    return True


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        output_filename = f'output_{filename}'
        output_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        save_status = minioClient.save_resource(app.config['UPLOAD_FOLDER'], upload_path)
        if not save_status:
            return jsonify({"error": "Failed to upload original video"}), 500

        thumbnail_upload_path = upload_path + thumbnail_file_extension
        extract_status=extract_first_frame(upload_path,thumbnail_upload_path)
        if not extract_status:
            return jsonify({"error": "Failed to extract image"}), 500
        save_status = minioClient.save_resource(app.config['UPLOAD_FOLDER'], thumbnail_upload_path)
        if not save_status:
            return jsonify({"error": "Failed to upload extracted image"}), 500

        if process_video(upload_path, output_path):
            save_status = minioClient.save_resource(app.config['RESULT_FOLDER'], output_path)
            if not save_status:
                return jsonify({"error": "Failed to upload processed video"}), 500
            thumbnail_output_path = output_path + thumbnail_file_extension
            extract_status = extract_first_frame(output_path,thumbnail_output_path)
            if not extract_status:
                return jsonify({"error": "Failed to extract processed video"}), 500
            save_status = minioClient.save_resource(app.config['RESULT_FOLDER'], thumbnail_output_path)
            if not save_status:
                return jsonify({"error": "Failed to  upload extracted processed video"}), 500
            return jsonify({"message": "File processed successfully", "output_file": output_filename}), 200
        else:
            return jsonify({"error": "Failed to process video"}), 500

@app.route('/media/<bucket>/file/<path:filename>', methods=['GET'])
def download_file(bucket,filename):
    try:
        data = minioClient.get_resource(bucket,filename)
        return data.read(), 200, {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    except:
        return jsonify({"error": "error to get file"}), 500


if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000)