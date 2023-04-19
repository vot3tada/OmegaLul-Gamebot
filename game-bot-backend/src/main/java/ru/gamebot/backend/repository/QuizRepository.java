package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Quiz;

public interface QuizRepository extends JpaRepository<Quiz,Integer> {
}

