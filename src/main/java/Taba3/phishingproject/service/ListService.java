package Taba3.phishingproject.service;

import Taba3.phishingproject.entity.PredictedList;
import Taba3.phishingproject.repository.BlackListRepository;
import Taba3.phishingproject.repository.PredictedListRepository;
import Taba3.phishingproject.repository.WhiteListRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.util.Collections;
import java.util.Map;

@Service
@Transactional
@RequiredArgsConstructor
public class ListService {
    private final BlackListRepository blackRepo;
    private final WhiteListRepository whiteRepo;
    private final PredictedListRepository predictedRepo;

    public PredictedList predictDangerPercentage(String url) {
        String aiServerUrl = "http://your-ai-server-ip:5000/predict";
        RestTemplate restTemplate = new RestTemplate();
        // AI 서버에 POST 요청 보내기
        ResponseEntity<Map> response = restTemplate.postForEntity(aiServerUrl, Collections.singletonMap("url", url), Map.class);
        Map<String, Object> responseBody = response.getBody();
        PredictedList predictedUrl = findUrl(url);
        if (responseBody != null && responseBody.containsKey("prediction")) {
           predictedUrl.setPercentage ((double) responseBody.get("prediction"));
            return predictedUrl;
        }
        return predictedUrl;
    }

    public boolean checkBlackUrl(String url){
        return blackRepo.existsByUrl(url);
    }
    public boolean checkWhiteUrl(String url){
        return whiteRepo.existsByUrl(url);
    }
    public boolean checkPredictedUrl(String url){
        return predictedRepo.existsByUrl(url);
    }
    public PredictedList findUrl (String url){
        return predictedRepo.findByUrl(url);
    }
}

