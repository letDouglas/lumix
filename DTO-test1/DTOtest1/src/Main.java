import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class Main {
    public static void main(String[] args) {
        String imagePath = System.getProperty("user.home") + "/Downloads/test.png";

        try {
            BufferedImage image = ImageIO.read(new File(imagePath));

            if (image != null) {
                ImageDTO imageDTO = new ImageDTO();
                imageDTO.setImageData(toByteArray(image));
                imageDTO.setFileName(extractFileName(imagePath));
                imageDTO.setContentType(determineContentType(imagePath));
                imageDTO.setFileSize(new File(imagePath).length());
                imageDTO.setWidth(image.getWidth());
                imageDTO.setHeight(image.getHeight());

                System.out.println("File Name: " + imageDTO.getFileName());
                System.out.println("Content Type: " + imageDTO.getContentType());
                System.out.println("File Size: " + imageDTO.getFileSize() + " bytes");
                System.out.println("Width: " + imageDTO.getWidth() + " pixels");
                System.out.println("Height: " + imageDTO.getHeight() + " pixels");
            } else {
                System.out.println("Failed to load the image.");
            }
        } catch (IOException e) {
            System.err.println("Error reading image file: " + e.getMessage());
        }
    }

    //BufferedImage to ByteArray
    private static byte[] toByteArray(BufferedImage image) throws IOException {
        // Use ByteArrayOutputStream and ImageIO.write to convert BufferedImage to byte array
        java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();
        String formatName = "png"; // You can dynamically determine this if needed
        ImageIO.write(image, formatName, baos);
        return baos.toByteArray();
    }

    //Extract file name
    private static String extractFileName(String imagePath) {
        File file = new File(imagePath);
        return file.getName();
    }

    //Determine content type based on file extension
    private static String determineContentType(String imagePath) {
        String extension = imagePath.substring(imagePath.lastIndexOf('.') + 1);
        return "image/" + extension;
    }
}
