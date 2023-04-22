package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Boss;

public interface BossRepository extends JpaRepository<Boss,Integer> {
}
