package Taba3.phishingproject.service;

import Taba3.phishingproject.entity.BlackList;
import Taba3.phishingproject.entity.PredictedList;
import Taba3.phishingproject.repository.BlackListRepository;
import Taba3.phishingproject.repository.PredictedListRepository;
import Taba3.phishingproject.repository.WhiteListRepository;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
@RequiredArgsConstructor
public class ListService {
    private final BlackListRepository blackRepo;
    private final WhiteListRepository whiteRepo;
    private final PredictedListRepository predictedRepo;

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

