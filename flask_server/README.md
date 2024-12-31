# Unity-to-Flask Image Upload API 📸

This project demonstrates how to upload images from a Unity3D application to a Flask server. The Flask server receives the image, validates it, and saves it to a designated **uploads** folder.  

---

## **1. Project Structure** 📂
```
UnityToFlask/
├── flask_server/
│   ├── app.py                 # Flask server code
│   ├── uploads/               # Folder to store uploaded images
│   ├── requirements.txt       # Python dependencies
│   ├── README.md              # Project documentation
└── unity_client/
    ├── Assets/
    │   ├── Scripts/
    │   │   ├── ImageUploader.cs   # Unity C# script for HTTP POST requests
    │   ├── StreamingAssets/       # Folder for test image
    ├── UnityProject.sln           # Unity project file
```

---

## **2. Flask Server Setup** 🖥️

### **Step 1: Install Dependencies**  
Navigate to the `flask_server` folder and install the required Python packages:  

```bash
pip install -r requirements.txt
```

**Contents of requirements.txt:**
```
flask
flask-cors
werkzeug
```

### **Step 2: Run the Flask Server**  
Start the server by running:  

```bash
python app.py
```

The server will run at:  
```
http://<YOUR_IP>:5000
```

---

## **3. Unity Client Setup** 🎮

### **Step 1: Add the Script**  
Place the following script in **Assets/Scripts/ImageUploader.cs**:

```csharp
using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class ImageUploader : MonoBehaviour
{
    // Server URL (replace with Flask server IP)
    private string uploadURL = "http://<YOUR_IP>:5000/upload";

    // File name and path
    public string fileName = "testImage.png";

    void Start()
    {
        // Start uploading image
        StartCoroutine(UploadImage());
    }

    IEnumerator UploadImage()
    {
        // Load image from StreamingAssets folder
        string filePath = System.IO.Path.Combine(Application.streamingAssetsPath, fileName);
        byte[] imageData = System.IO.File.ReadAllBytes(filePath);

        // Create form-data
        WWWForm form = new WWWForm();
        form.AddBinaryData("file", imageData, fileName, "image/png");

        // Send HTTP POST request
        using (UnityWebRequest request = UnityWebRequest.Post(uploadURL, form))
        {
            yield return request.SendWebRequest();

            // Handle response
            if (request.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("Upload successful: " + request.downloadHandler.text);
            }
            else
            {
                Debug.LogError("Upload failed: " + request.error);
            }
        }
    }
}
```

### **Step 2: Add Image in Unity**  
1. Place a test image named `testImage.png` in the **StreamingAssets** folder:  
   ```
   UnityToFlask/unity_client/Assets/StreamingAssets/testImage.png
   ```

2. Attach the **ImageUploader.cs** script to a GameObject in Unity.  

3. Play the Unity scene to test the upload.

---

## **4. Test the API** 🧪

### **Using Postman or CURL**
**POST URL:**
```
http://<YOUR_IP>:5000/upload
```

**Headers:**
```
Content-Type: multipart/form-data
```

**Body (form-data):**
```
Key: file
Value: Select Image File
```

**CURL Example:**
```bash
curl -X POST http://<YOUR_IP>:5000/upload \
-F "file=@path_to_your_image/testImage.png"
```

---

## **5. Uploaded Files Location** 📁

All uploaded images are stored in the **uploads/** folder within the Flask server directory:

```
flask_server/uploads/
```

Example:
```
flask_server/uploads/testImage.png
```

---

## **6. Security Notes** 🔒

1. **CORS Support:**  
   The server supports external requests via Flask-CORS.  
2. **File Type Validation:**  
   Only images (PNG, JPG, JPEG, GIF) are allowed.  
3. **File Size Limit:**  
   Uploads are restricted to **16 MB**.  
4. **Filename Safety:**  
   Uses `werkzeug.utils.secure_filename()` to prevent malicious filenames.  
5. **HTTPS Support (Optional):**  
   Use a reverse proxy (e.g., Nginx) for SSL certificates in production.

---

## **7. Known Issues** 🛠️
1. **Timeouts with Large Files:**  
   Increase server timeout settings if uploading larger files.  
2. **Cross-Origin Errors:**  
   Verify that CORS is enabled in the Flask server and the client specifies the correct server URL.

---

## **8. Next Steps 🚀**
- **Authentication:** Add API keys or JWT tokens for access control.  
- **Download API:** Implement endpoints to retrieve uploaded images.  
- **Image Processing:** Integrate image resizing or compression before saving.  

---

## **9. Contact** 📧

For any questions or suggestions, feel free to reach out.  
- **Author:** Vishnu Sivan  
- **Email:** [your_email@example.com]  
- **LinkedIn:** [Your LinkedIn Profile](https://www.linkedin.com)

---

Let me know if you need additional sections or edits!