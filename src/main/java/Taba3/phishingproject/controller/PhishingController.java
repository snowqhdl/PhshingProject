package Taba3.phishingproject.controller;


import Taba3.phishingproject.service.ListService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/validation")
@RequiredArgsConstructor
public class PhishingController {
    private final ListService service;

    @GetMapping("/check")
    public ResponseEntity validation(@RequestParam(value = "url") String url) {
        String result = service.predictDangerPercentage(url);
        return ResponseEntity.ok(result);
    }
}