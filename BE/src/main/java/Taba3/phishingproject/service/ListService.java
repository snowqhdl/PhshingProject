package Taba3.phishingproject.service;

import Taba3.phishingproject.entity.PredictedList;
import Taba3.phishingproject.repository.BlackListRepository;
import Taba3.phishingproject.repository.PredictedListRepository;
import Taba3.phishingproject.repository.WhiteListRepository;
import lombok.RequiredArgsConstructor;
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
            return "안전한 사이트입니다. 안심하고 이용하세요!";
        } else if (checkBlackUrl(url)){
            return "주의! 이 사이트는 피싱 위험이 있습니다!";
        } else if (checkPredictedUrl(url)) {
            return "주의! 이 사이트는 피싱 위험이 있습니다!";
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

