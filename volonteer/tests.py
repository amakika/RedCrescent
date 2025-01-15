import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dtiijcqnw",
    api_key="679278777566463",
    api_secret="d-uMGdK1jqyNbaRnP64HvCsuKJc"
)

response = cloudinary.uploader.upload("/home/yasin/RedCresentt/volonteer/бабушки.jpg")
print("Upload successful:", response["url"])

# Create your tests here.
