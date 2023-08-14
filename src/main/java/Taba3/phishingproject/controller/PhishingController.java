package Taba3.phishingproject.controller;


import Taba3.phishingproject.dto.BlackListDto;
import Taba3.phishingproject.entity.BlackList;
import Taba3.phishingproject.mapper.ListMapper;
import Taba3.phishingproject.service.ListService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/validation")
@RequiredArgsConstructor
public class PhishingController {
    private final ListMapper mapper;
    private final ListService service;

    @GetMapping
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