package Taba3;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;

@SpringBootApplication
//@EntityScan("your.package.name")
public class PhishingProjectApplication {

	public static void main(String[] args) {
		SpringApplication.run(PhishingProjectApplication.class, args);
	}

}
