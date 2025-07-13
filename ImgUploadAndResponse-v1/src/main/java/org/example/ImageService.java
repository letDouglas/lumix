package org.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;

@Service
public class ImageService {

    @Autowired
    private InMemoryBucketService inMemoryBucketService;

    public ImageDTO processImage(MultipartFile file) {
        try {
            byte[] byteArray = file.getBytes();
            String fileName = file.getOriginalFilename();
            String fileType = file.getContentType();
            long fileSize = file.getSize();

            BufferedImage bufferedImage = ImageIO.read(file.getInputStream());
            int height = bufferedImage.getHeight();
            int width = bufferedImage.getWidth();

            // Extract pixel array from BufferedImage
            int[] pixelArray = bufferedImage.getRGB(0, 0, width, height, null, 0, width);

            // Upload the file to the in-memory bucket
            inMemoryBucketService.uploadFile(fileName, byteArray);

            return new ImageDTO(byteArray, fileName, fileType, fileSize, height, width, pixelArray);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
