package Taba3.phishingproject.entity;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

import javax.persistence.*;

@Entity
@RequiredArgsConstructor
@Getter
@Setter
public class PredictedList {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long predictedUrlId;

    @Column(nullable = false)
    private String url;

    @Column(nullable = false)
    private double percentage;

}
