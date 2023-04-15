package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.gamebot.backend.models.Task;

public interface TaskRepository extends JpaRepository<Task, Integer> {
}
