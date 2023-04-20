package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Effect;
@Repository
public interface EffectRepository extends JpaRepository<Effect, Integer> {
}
