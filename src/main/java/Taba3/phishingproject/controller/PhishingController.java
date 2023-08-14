package Taba3.phishingproject.controller;


import Taba3.phishingproject.mapper.ListMapper;
import Taba3.phishingproject.service.ListService;
import lombok.AllArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/validation")
@RequiredArgsConstructor
public class PhishingController {
    private final ListMapper mapper;
    private final ListService service;

    @GetMapping("/check")
    public ResponseEntity validation(@RequestParam(value = "url") String url) {
        if (service.checkBlackUrl(url)) {
            return ResponseEntity.ok("Phishing site");
        } else if (service.checkWhiteUrl(url)) {
            return ResponseEntity.ok("White site");
        } else if (service.checkPredictedUrl(url)) {
            return new ResponseEntity<>(mapper.predictedListToResponse(service.findUrl(url)), HttpStatus.OK);

        } else
            return new ResponseEntity<>(mapper.predictedListToResponse(service.predictDangerPercentage(url)), HttpStatus.OK);

    }
}