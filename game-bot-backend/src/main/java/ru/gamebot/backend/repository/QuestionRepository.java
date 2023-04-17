package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Question;

public interface QuestionRepository extends JpaRepository<Question,Integer> {
}
