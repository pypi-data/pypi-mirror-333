# **Ventral Vision API Client** 🚀
A **lightweight, no-code-friendly vision API** for **object detection and segmentation**. Easily integrate it into your projects with just a few lines of code!  


![vision-api-banner](https://ventral.ai/wp-content/uploads/2024/08/Ventral_Vision_AI_1_-removebg-preview-e1724758129283.png) 

## **✨ Features**  
✅ **Plug & Play** – Simple API integration with Python & JavaScript clients  
✅ **Ultra Low-Cost** – Affordable pricing with **Jetson-based cloud inference**  
✅ **Customizable** – Train & label your own models easily  
✅ **On-Site Ready** – Deploy locally if needed  

## **📦 Installation**  
### **Python Client**  
```bash
pip install vision-api-client
```

### **JavaScript Client**
```bash
npm install vision-api-client
```

## **🚀 Quickstart**
### **Python Example**
```python
from vision_api_client import VisionAPI

api = VisionAPI(api_key="your_api_key")

# Upload an image for object detection
response = api.detect_objects("image.jpg")
print(response)
```

### **JavaScript Example**
```javascript
import VisionAPI from "vision-api-client";

const api = new VisionAPI("your_api_key");

// Upload an image for object detection
api.detectObjects("image.jpg").then(console.log);
```

## **📡 API Endpoints**
| Method | Endpoint  | Description                     |
|--------|-----------|---------------------------------|
| POST   | /detect   | Detect objects in an image      |
| POST   | /segment  | Perform image segmentation      |
📖 View full API documentation → TBD

## **💰 Pricing**
| Plan     | Price   | Usage Limit                          |
|----------|---------|--------------------------------------|
| Free     | $0      | Limited calls per month              |
| Standard | $20/mo  | More API calls & priority support    |
| Pro      | $99/mo  | High usage & premium support         |
🔗 Subscribe here

## **📢 Get Started Today!**
Sign up at ventral.ai and get your FREE API key today! 🚀