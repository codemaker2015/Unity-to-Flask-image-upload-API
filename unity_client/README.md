# Unity3D File Upload Demo

```cs
using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
using System.IO; 
public class UploadImage : MonoBehaviour
{
    public string serverUrl = "http://192.168.29.130:5000/upload"; // Replace with your server URL

    void Start()
    {
        
    }

    public void Upload() {
        StartCoroutine(UploadImageFromStreamingAssets("logo.jpg"));
    }

    IEnumerator UploadImageFromStreamingAssets(string imageName)
    {
        // Get the file path
        string filePath = Path.Combine(Application.streamingAssetsPath, imageName);

        // Handle Android path
        byte[] imageData;

        if (filePath.Contains("://") || filePath.Contains(":///"))
        {
            UnityWebRequest www = UnityWebRequest.Get(filePath);
            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                imageData = www.downloadHandler.data;
            }
            else
            {
                Debug.LogError("Failed to load file: " + www.error);
                yield break;
            }
        }
        else
        {
            // For Windows, Mac, Linux
            imageData = File.ReadAllBytes(filePath);
        }

        // Create Form Data
        WWWForm form = new WWWForm();
        form.AddBinaryData("file", imageData, imageName, "image/jpg");

        // Upload the image
        using (UnityWebRequest uploadRequest = UnityWebRequest.Post(serverUrl, form))
        {
            yield return uploadRequest.SendWebRequest();

            if (uploadRequest.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("Upload successful: " + uploadRequest.downloadHandler.text);
            }
            else
            {
                Debug.LogError("Upload failed: " + uploadRequest.error);
            }
        }
    }
}
```