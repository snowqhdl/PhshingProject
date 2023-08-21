package Taba3.phishingproject.repository;

import Taba3.phishingproject.entity.PredictedList;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PredictedListRepository extends JpaRepository<PredictedList, Long> {
    boolean existsByUrl(String url);
    PredictedList findByUrl(String url);
}
