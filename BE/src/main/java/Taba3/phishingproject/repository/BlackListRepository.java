package Taba3.phishingproject.repository;

import Taba3.phishingproject.entity.BlackList;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BlackListRepository extends JpaRepository<BlackList,Long> {
    boolean existsByUrl(String url);
}
