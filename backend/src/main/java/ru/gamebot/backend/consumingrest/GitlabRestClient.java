package ru.gamebot.backend.consumingrest;

import lombok.Data;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import ru.gamebot.backend.dto.GitLabContributionDTO;
import ru.gamebot.backend.dto.GitLabUserDTO;
import ru.gamebot.backend.util.exceptions.GitlabCleintExceptions.GitlabUserNotFound;

import java.time.Instant;
import java.time.temporal.ChronoUnit;

@Component
@Data
public class GitlabRestClient {

    public Long getGitLabUserId(String userName) throws GitlabUserNotFound {
        ResponseEntity<GitLabUserDTO[]> response = new RestTemplate().getForEntity(String.format(
                "https://gitlab.com/api/v4/users/?username=%s", userName), GitLabUserDTO[].class);
        if(response.getBody().length == 0 ){
            throw new GitlabUserNotFound("909");
        }
        return response.getBody()[0].getId();
    }

    public GitLabContributionDTO[] getUserActivity(Long userGitLabId) {
        ResponseEntity<GitLabContributionDTO[]> response =
                new RestTemplate().getForEntity(String.format(
                                "https://gitlab.com/api/v4/users/%d/events?after=%s&before=%s",
                                userGitLabId, Instant.now().minus(1, ChronoUnit.DAYS),
                                Instant.now().plus(1, ChronoUnit.DAYS)),
                        GitLabContributionDTO[].class);
        return response.getBody();
    }

}