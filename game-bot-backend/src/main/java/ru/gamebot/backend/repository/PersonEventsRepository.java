package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.PersonEvents;
@Repository
public interface PersonEventsRepository extends JpaRepository<PersonEvents, Integer> {
}
