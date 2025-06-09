package org.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

@org.springframework.stereotype.Controller
public class Controller {

    @Autowired
    private ImageService imageService;

    @Autowired
    private Evaluer evaluer;

    @Autowired
    private ResponseLogic responseLogic;

    @GetMapping("/")
    public String index() {
        return "upload";
    }

    @PostMapping("/upload")
    public String uploadImage(@RequestParam("file") MultipartFile file, Model model) {
        if (file.isEmpty()) {
            model.addAttribute("error", "ERROR: No file selected");
            return "upload";
        }

        try {
            ImageDTO imageDTO = imageService.processImage(file);
            boolean evaluationResult = evaluer.evaluate(imageDTO);
            responseLogic.setMeetsCriteria(evaluationResult);

            if (!evaluationResult) {
                model.addAttribute("error", "ERROR: Image too big or wrong file type");
                return "upload";
            }

            model.addAttribute("imageDTO", imageDTO);
            model.addAttribute("meetsCriteria", responseLogic.isMeetsCriteria());
        } catch (Exception e) {
            e.printStackTrace();
            model.addAttribute("error", "ERROR: An unexpected error occurred");
            return "upload";
        }

        return "result";
    }
}