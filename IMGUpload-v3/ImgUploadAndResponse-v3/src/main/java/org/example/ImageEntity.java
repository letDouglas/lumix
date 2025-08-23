package org.example;

import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;

@Entity
@Table(name = "images")
public class ImageEntity {             // PORCO DIO PORCO DIO INFAME BASTARDO MADONNA FOTTUTA TROIA

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String fileName;
    private String fileType;
    private long fileSize;
    private int height;
    private int width;
    private String s3ObjectKey; // This will store the S3 object key/code

    // Constructors, getters, and setters
    public ImageEntity() {}

    public ImageEntity(String fileName, String fileType, long fileSize, int height, int width, String s3ObjectKey) {
        this.fileName = fileName;
        this.fileType = fileType;
        this.fileSize = fileSize;
        this.height = height;
        this.width = width;
        this.s3ObjectKey = s3ObjectKey;
    }

    // Getters and setters for all fields
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getFileName() { return fileName; }
    public void setFileName(String fileName) { this.fileName = fileName; }
    public String getFileType() { return fileType; }
    public void setFileType(String fileType) { this.fileType = fileType; }
    public long getFileSize() { return fileSize; }
    public void setFileSize(long fileSize) { this.fileSize = fileSize; }
    public int getHeight() { return height; }
    public void setHeight(int height) { this.height = height; }
    public int getWidth() { return width; }
    public void setWidth(int width) { this.width = width; }
    public String getS3ObjectKey() { return s3ObjectKey; }
    public void setS3ObjectKey(String s3ObjectKey) { this.s3ObjectKey = s3ObjectKey; }
}
