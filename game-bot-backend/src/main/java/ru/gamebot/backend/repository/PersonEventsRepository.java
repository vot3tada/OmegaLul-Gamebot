package ru.gamebot.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.gamebot.backend.models.Event;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.models.PersonEvents;

import java.util.Date;
import java.util.List;

@Repository
public interface PersonEventsRepository extends JpaRepository<PersonEvents, Integer> {
    List<PersonEvents> findAllByEvent(Event event);
    void deleteByEventAndPerson(Event event, Person person);
    List<PersonEvents> findAllEventByPersonPersonPkChatIdAndEventStartedAtAfterOrderByEventDesc(Integer id, Date date);
}
