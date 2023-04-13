package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Effect;

public interface EffectRepository extends JpaRepository<Effect, Integer> {
}
