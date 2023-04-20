package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.AchievementDTO;
import ru.gamebot.backend.dto.PersonAchievementDTO;
import ru.gamebot.backend.models.PersonPK;
import ru.gamebot.backend.repository.AchievementRepository;
import ru.gamebot.backend.repository.PersonRepository;
import ru.gamebot.backend.util.exceptions.AchievementExceptions.AchievementNotFoundException;
import ru.gamebot.backend.util.exceptions.PersonExceptions.PersonNotFoundException;
import ru.gamebot.backend.util.mappers.AchievementMapper.AchievementMapper;

import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class AchievementService {

    private final AchievementRepository achievementRepository;
    private final AchievementMapper achievementMapper;

    private final PersonRepository personRepository;

    public AchievementDTO getAchievementById(String id){
        return achievementMapper.achievementToAchievementDTO(
                                achievementRepository.findById(id).
                                orElseThrow(AchievementNotFoundException::new));
    }

    public List<AchievementDTO> getPersonAchievements(Integer chatId, Integer userId){
        var person = personRepository.findById(new PersonPK(chatId, userId))
                                    .orElseThrow(PersonNotFoundException::new);
        return person.getAchievements().stream().map(achievementMapper::achievementToAchievementDTO).toList();
    }

    @Transactional
    public void addAchievementToPerson(PersonAchievementDTO personAchievementDTO){
        var person = personRepository.findById(new PersonPK(personAchievementDTO.getChatId()
                                            ,personAchievementDTO.getUserId()))
                                            .orElseThrow(PersonNotFoundException::new);
        person.getAchievements().add(achievementRepository.findById(personAchievementDTO.getAchievementId())
                                    .orElseThrow(AchievementNotFoundException::new));
        personRepository.save(person);
    }
}

