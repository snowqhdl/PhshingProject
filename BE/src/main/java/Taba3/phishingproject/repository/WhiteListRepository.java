package Taba3.phishingproject.repository;

import Taba3.phishingproject.entity.WhiteList;
import org.springframework.data.jpa.repository.JpaRepository;

public interface WhiteListRepository extends JpaRepository<WhiteList, Long> {
    boolean existsByUrl(String url);
}
