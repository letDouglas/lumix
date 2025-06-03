public class ImageDTO {
    private byte[] imageData;
    private String fileName;
    private String contentType;
    private long fileSize;
    private int width;
    private int height;

    public ImageDTO() {
    }

    public ImageDTO(byte[] imageData, String fileName, String contentType, long fileSize, int width, int height) {
        this.imageData = imageData;
        this.fileName = fileName;
        this.contentType = contentType;
        this.fileSize = fileSize;
        this.width = width;
        this.height = height;
    }

    public byte[] getImageData() {
        return imageData;
    }

    public void setImageData(byte[] imageData) {
        this.imageData = imageData;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getContentType() {
        return contentType;
    }

    public void setContentType(String contentType) {
        this.contentType = contentType;
    }

    public long getFileSize() {
        return fileSize;
    }

    public void setFileSize(long fileSize) {
        this.fileSize = fileSize;
    }

    public int getWidth() {
        return width;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    public int getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }
}
