package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Work;
@Repository
public interface WorkRepository extends JpaRepository<Work, Integer> {
    Boolean existsByName(String name);
}
