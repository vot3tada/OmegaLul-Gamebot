package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Event;

import java.time.LocalDateTime;

@Repository
public interface EventRepository extends JpaRepository<Event, Integer> {
    Boolean existsByNameAndStartedAt(String name, LocalDateTime date);
}
