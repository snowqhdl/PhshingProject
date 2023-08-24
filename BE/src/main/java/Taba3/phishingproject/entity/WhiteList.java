package Taba3.phishingproject.entity;

import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;

import javax.persistence.*;

@Entity
@RequiredArgsConstructor
@Getter
@Setter
public class WhiteList {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long whiteUrlId;

    @Column(nullable = false, unique = true)
    private String url;
}
