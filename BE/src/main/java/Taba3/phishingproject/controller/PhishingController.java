package Taba3.phishingproject.controller;


import Taba3.phishingproject.service.ListService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/validation")
@RequiredArgsConstructor
public class PhishingController {
    private final ListService service;

    @CrossOrigin(origins = "http://localhost:5173/")
    @GetMapping("/check")
    public ResponseEntity validation(@RequestParam(value = "url") String url) {
        String result = service.predictDangerPercentage(url);
        return ResponseEntity.ok(result);
    }
}