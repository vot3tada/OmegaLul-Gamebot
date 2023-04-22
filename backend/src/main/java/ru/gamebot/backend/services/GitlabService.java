package ru.gamebot.backend.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.consumingrest.GitlabRestClient;
import ru.gamebot.backend.dto.GetGitlabDTO;
import ru.gamebot.backend.dto.GitLabContributionDTO;
import ru.gamebot.backend.models.Person;
import ru.gamebot.backend.repository.PersonRepository;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@Transactional
public class GitlabService {
    private final PersonRepository personRepository;
    private final GitlabRestClient gitlabRestClient;
    private final Map<String, String> translateMap = new HashMap<>();
    @Autowired
    public GitlabService(PersonRepository personRepository, GitlabRestClient gitlabRestClient){
        this.gitlabRestClient = gitlabRestClient;
        this.personRepository = personRepository;
        translateMap.put("approved","Одобрил merge request");
        translateMap.put("opened","Создал merge request");
        translateMap.put("accepted","Слил ветку");
        translateMap.put("pushed","Запушил commit");
    }
    public List<GetGitlabDTO> getUsersStats(Integer chatId){
        var persons = personRepository.findByPersonPkChatIdAndGitlabIdIsNotNull(chatId);
        var resultList = new ArrayList<GetGitlabDTO>();
        for(Person person : persons){
            var contributions = gitlabRestClient.getUserActivity(person.getGitlabId());
            if (contributions.length == 0){
                continue;
            }
            resultList.add(new GetGitlabDTO(person.getPersonPk().getUserId(),countEachAction(contributions)));
        }
        return  resultList;
    }

    private List<GetGitlabDTO.Contribution> countEachAction(GitLabContributionDTO[] activities){
        var activityCount = new HashMap<String,Integer>();
        var contributions = new ArrayList<GetGitlabDTO.Contribution>();
        for (GitLabContributionDTO activity : activities) {
            activity.splitActionName();
            activityCount.putIfAbsent(activity.getActionName(), 0);
            activityCount.put(activity.getActionName(), activityCount.get(activity.getActionName()) + 1);
        }
        for(Map.Entry<String,Integer> entry: activityCount.entrySet()){
            contributions.add(new GetGitlabDTO.Contribution(translateMap.get(entry.getKey()), entry.getValue()));
        }
        return contributions;
    }

}
