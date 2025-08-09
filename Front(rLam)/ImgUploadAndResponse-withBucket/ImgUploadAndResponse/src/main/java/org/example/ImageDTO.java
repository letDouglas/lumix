package org.example;

public class ImageDTO {
    private byte[] byteArray;
    private String fileName;
    private String fileType;
    private long fileSize;
    private int height;
    private int width;
    private int[] pixelArray;

    public ImageDTO() {
    }

    public ImageDTO(byte[] byteArray, String fileName, String fileType, long fileSize, int height, int width, int[] pixelArray) {
        this.byteArray = byteArray;
        this.fileName = fileName;
        this.fileType = fileType;
        this.fileSize = fileSize;
        this.height = height;
        this.width = width;
        this.pixelArray = pixelArray;
    }

    public byte[] getByteArray() {
        return byteArray;
    }

    public void setByteArray(byte[] byteArray) {
        this.byteArray = byteArray;
    }

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public long getFileSize() {
        return fileSize;
    }

    public void setFileSize(long fileSize) {
        this.fileSize = fileSize;
    }

    public int getHeight() {
        return height;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public int getWidth() {
        return width;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    public int[] getPixelArray() {
        return pixelArray;
    }

    public void setPixelArray(int[] pixelArray) {
        this.pixelArray = pixelArray;
    }
}
