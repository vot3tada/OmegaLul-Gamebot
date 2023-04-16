package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Event;
@Repository
public interface EventRepository extends JpaRepository<Event, Integer> {
}
