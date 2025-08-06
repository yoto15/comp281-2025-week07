### python packeage
- flask
- python-dotenv
- numpy
- opencv-python-headless

### flask template ใน Week07
```
flask
├──static
|	├──cg-module.js
|	├──workshop01.js
|	├──workshop02.js
|	└──workshop03.js
├──templates
|	├──index.html
|	├──workshop01.html
|	├──workshop02.html
|	└──workshop03.html
├──app.py
└──imgcvt.py
```
### Workshops
### Workshop01 - Image Transfer
- (frontend) ส่งภาพไป backend ด้วย BASE64 string
- (backend) รับ BASE64 → แปลงเป็น numpy array → แปลงเป็น OpenCV image → แปลงกลับเป็น BASE64 เพื่อส่งคืน
- (frontend) รับภาพจาก backend แล้วแสดงใน `<img>` หรือ `<canvas>`
---
### Workshop02 - Color Space Conversion
- ใช้ความรู้จาก Workshop01
- (backend) ใช้ OpenCV แปลงโหมดสีของภาพ (เช่น BGR → GRAY, HSV) แล้วส่งกลับมาให้แสดงผล
---
### Workshop03 - Image Filtering
- ใช้ความรู้จาก Workshop02
- (backend) ใช้ OpenCV ทำ image filtering เช่น blur, sharpen, Canny edge, threshold แล้วส่งผลลัพธ์กลับมาแสดง
---

### web page feature using
- `<input type="file">`
- `<img>`, select image file to server
- `<video>`, webcam (WebRTC) snapshot image to server

### OpenCV
Docs: https://docs.opencv.org/4.12.0/

Python: https://docs.opencv.org/4.12.0/d6/d00/tutorial_py_root.html

### OpenCV Image Color-space

หลักๆใน OpenCV Image จะมีการเรียงลำดับของช่องสี (Color Channel) เรียงจาก Blue -> Green -> Red หรือเรียกว่า BGR ให้ผู้เรียนจำตรงส่วนนี้ไว้ให้ดี โดยตามปกติสีจะเป็นแบบ RGB อาจขัดด้านความเคยชิน แต่ต้องเข้าใจว่าเป็นสิ่งที่ OpenCV กำหนดในการใช้งานมานานมากแล้ว

โดยการจัดการเรื่อง Color-space นั้นจะได้คำสั่ง
```
cv.cvtColor(<src>, <code>) -> <dest>
<src> = ภาพต้นฉบับ
<code> = โหมดสี
<dest> = ภาพผลลัพธ์
```
- โหมดสี [Docs](https://docs.opencv.org/4.12.0/d8/d01/group__imgproc__color__conversions.html#ga4e0972be5de079fed4e3a10e24ef5ef0)

### OpenCV Image Filter มี 2 กลุ่ม
### []()
### กลุ่ม 1: Filter สำหรับ “ปรับภาพ” (ใช้ได้กับ 3 ช่อง BGR)

```
cv2.GaussianBlur()
```
ทำอะไร: ทำให้ภาพนุ่มลง ละลายรายละเอียดเล็ก ๆ (smooth ภาพ)

ทำงานยังไง: ใช้ Gaussian kernel (กระจายตาม bell curve) กระจายค่าสีไปรอบ ๆ จุดนั้น

ใช้ทำอะไร: ลด noise ก่อนตรวจจับขอบ, ทำให้หน้าเนียน (beauty cam), เตรียมภาพให้ model ใช้ (denoising)

```
cv2.blur() หรือ cv2.boxFilter()
```
ทำอะไร: เบลภาพด้วยวิธีเฉลี่ยสีรอบ ๆ แบบง่าย ๆ

ทำงานยังไง: เฉลี่ยค่าสีรอบจุดนั้นในกรอบ เช่น 5x5

ใช้ทำอะไร: ลดรายละเอียดเล็ก ๆ เหมือน GaussianBlur แต่ไม่เนียนเท่า หรือคือ "blur แบบง่ายๆ

```
cv2.medianBlur()
```
ทำอะไร: ลบจุดรบกวนเล็ก ๆ เช่น "salt and pepper noise"

ทำงานยังไง: เลือกค่ากลางของ pixel ในกรอบ (ไม่ใช่เฉลี่ย)

ใช้ทำอะไร: ลบจุด noise เล็ก ๆ โดยไม่เบลทั้งภาพ, เหมาะกับภาพที่มีจุดดำ/ขาวกระจาย

```
cv2.filter2D()
```
ทำอะไร: ใช้ kernel แบบ custom ได้ (sharpen, emboss, etc.)

ทำงานยังไง: นำ kernel 2D ไป convolve กับภาพ

ใช้ทำอะไร: ทำ filter เองได้ตามต้องการ

ตัวอย่าง kernel:
- sharpen: [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
- emboss: [[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]

```
cv2.bitwise_not() / cv2.bitwise_and() / cv2.bitwise_or()
```
ทำอะไร: ทำภาพเชิงบิต เช่นกลับสี (invert) หรือเอา mask ไปซ้อน

ทำงานยังไง: ทำ AND / OR / NOT ทีละ pixel

ใช้ทำอะไร: ทำ mask เพื่อซ้อนภาพหรือแยกวัตถุ, สร้าง effect “ภาพเชิงลบ” หรือภาพสีตรงข้าม

### กลุ่ม 2: Filter สำหรับ “คำนวณ/วิเคราะห์” (ต้องแปลง grayscale ก่อน)

```
cv2.Canny()
```
ทำอะไร: หาขอบภาพแบบคมและแม่นยำ

ทำงานยังไง: ทำ 4 ขั้นตอน: blur → gradient → non-maximum suppression → hysteresis

ใช้ทำอะไร: หาขอบวัตถุ, ใช้ในระบบตรวจจับรูปร่าง, ขอบ, หรือใช้เป็น input ให้ AI

```
cv2.Sobel() และ cv2.Laplacian()
```
ทำอะไร: หาทิศทางขอบภาพ (gradient)

ทำงานยังไง:
```
Sobel = หาขอบแนว X, Y (หรือทั้งคู่)

Laplacian = หาความเปลี่ยนแปลงรวดเร็ว (ความโค้ง, ขอบ)
```
ใช้ทำอะไร: ใช้เป็น base ของการวิเคราะห์ภาพ, ทำ pre-processing ให้ AI หรือทำ effect ขอบในเกม

```
cv2.threshold() และ cv2.adaptiveThreshold()
```
ทำอะไร: เปลี่ยนภาพ grayscale → binary (ขาว/ดำ)

ทำงานยังไง:
```
threshold: ตัดค่าตามค่าเดียว เช่น ถ้า > 127 → 255

adaptiveThreshold: คำนวณจากบริเวณรอบ ๆ pixel → ดีกับแสงไม่สม่ำเสมอ
```

ใช้ทำอะไร: เตรียมภาพให้ contour หรือ OCR ใช้, แยกพื้นหลัง/ตัวอักษร

```
cv2.erode() / cv2.dilate()
```
ทำอะไร: ลบ/ขยายพื้นที่ของ pixel สีขาว

ทำงานยังไง:
```
Erode: ลบ pixel รอบนอก → หดวัตถุ

Dilate: เติม pixel รอบนอก → ขยายวัตถุ
```
ใช้ทำอะไร: ลบจุดรบกวน, เติมรอยขาดของตัวอักษร, ทำ mask ให้เนียนขึ้น