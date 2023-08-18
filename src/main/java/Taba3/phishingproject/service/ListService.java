package Taba3.phishingproject.service;

import Taba3.phishingproject.entity.PredictedList;
import Taba3.phishingproject.repository.BlackListRepository;
import Taba3.phishingproject.repository.PredictedListRepository;
import Taba3.phishingproject.repository.WhiteListRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

@Service
@Transactional
@RequiredArgsConstructor
public class ListService {

    private final BlackListRepository blackRepo;
    private final WhiteListRepository whiteRepo;
    private final PredictedListRepository predictedRepo;

    public String predictDangerPercentage(String url) {
        String AI_SERVER = "http://127.0.0.1:5001/predict";
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        String requestBody = "{\"url\": \"" + url + "\"}";
        HttpEntity<String> requestEntity = new HttpEntity<>(requestBody, headers);
        RestTemplate restTemplate = new RestTemplate();
        if (checkWhiteUrl(url)) {
            return "Whitelisted site";
        } else if (checkBlackUrl(url)) {
            return "Blacklisted site";
        } else if (checkPredictedUrl(url)) {
            return String.valueOf(findUrl(url).getPercentage());
        } else {
            // AI 서버로 API 호출
            ResponseEntity<String> response = restTemplate.exchange(AI_SERVER, HttpMethod.POST, requestEntity, String.class);
            return response.getBody();
        }
    }


        public boolean checkBlackUrl (String url){
            return blackRepo.existsByUrl(url);
        }
        public boolean checkWhiteUrl (String url){
            return whiteRepo.existsByUrl(url);
        }
        public boolean checkPredictedUrl (String url){
            return predictedRepo.existsByUrl(url);
        }
        public PredictedList findUrl (String url){
            return predictedRepo.findByUrl(url);
        }
    }

