package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Achievement;

public interface AchievementRepository extends JpaRepository<Achievement, String>{
}
