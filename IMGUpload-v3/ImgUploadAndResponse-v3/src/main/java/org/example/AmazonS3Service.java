package org.example;

import java.io.ByteArrayInputStream;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.s3.model.S3ObjectInputStream;
import com.amazonaws.util.IOUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@Service
public class AmazonS3Service {

    @Value("${aws.s3.bucket}")
    private String bucketName;

    @Autowired
    private AmazonS3 amazonS3;

    public boolean uploadFile(String fileName, byte[] fileContent) {
        try {
            ObjectMetadata metadata = new ObjectMetadata();
            metadata.setContentLength(fileContent.length);
            amazonS3.putObject(new PutObjectRequest(bucketName, fileName, new ByteArrayInputStream(fileContent), metadata));
            return true;
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public byte[] downloadFile(String fileName) {
        try {
            S3Object s3Object = amazonS3.getObject(bucketName, fileName);
            S3ObjectInputStream objectInputStream = s3Object.getObjectContent();
            return IOUtils.toByteArray(objectInputStream);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
