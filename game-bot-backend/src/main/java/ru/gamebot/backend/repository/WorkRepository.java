package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Work;

public interface WorkRepository extends JpaRepository<Work, Integer> {
    Work findByName(String name);
}
