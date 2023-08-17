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

@Service
@Transactional
@RequiredArgsConstructor
public class ListService {
    private final BlackListRepository blackRepo;
    private final WhiteListRepository whiteRepo;
    private final PredictedListRepository predictedRepo;
    private final RestTemplate restTemplate;

    private final String AI_SERVER = "http://your-ai-server-ip:5000/predict";

    public String predictDangerPercentage(String url) {
        if (checkWhiteUrl(url)) {
            return "Whitelisted site";
        } else if (checkBlackUrl(url)) {
            return "Blacklisted site";
        } else if (checkPredictedUrl(url)) {
            return String.valueOf(findUrl(url).getPercentage());
        } else {
            // AI 서버로 API 호출
            ResponseEntity<String> response = restTemplate.postForEntity(AI_SERVER, url, String.class);
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

