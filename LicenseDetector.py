from ultralytics import YOLO
import cv2
# import util
from util import get_car, read_license_plate, write_csv
vehicles = [2, 3, 5, 7]  # yoto classes that are vehicles
class LicenseDetector:

    def __init__(self):
        self.coco_model = YOLO('yolov8n.pt')
        self.license_plate_detector = YOLO('license_plate_detector.pt')

    def detect(self, filename):
        results = {}
        results[1] = {}
        # detect vehicles
        frame = cv2.imread(filename)  # IMG_20230704_082737.jpg") #
        detections = self.coco_model(frame)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score])

        # detect license plates
        license_plates = self.license_plate_detector(frame)[0]
        count = 0
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate
            start_point = (int(x1), int(y1))
            end_point = (int(x2), int(y2))
            color = (255, 0, 0)
            thickness = 2
        #   newFrame = cv2.rectangle(frame, start_point, end_point, color, 2)
        #    cv2.imwrite("out.jpg", newFrame)
            # crop license plate
            license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
        #    cv2.imwrite("out2.jpg", license_plate_crop)
            # process license plate
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
        #    cv2.imwrite("out3.jpg", license_plate_crop_gray)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
        #    cv2.imwrite("out4.jpg", license_plate_crop_thresh)
            # read license plate number
            license_plate_text="0"
            try:
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_gray)
                if license_plate_text is not None:
                    count += 1
                    results[count] = {'license_plate': {'bbox': [x1, y1, x2, y2],
                                        'text': license_plate_text,
                                        'bbox_score': score,
                                        'text_score': license_plate_text_score}}
            except BaseException:
                pass
            print(results)
            return license_plate_text
# write results
