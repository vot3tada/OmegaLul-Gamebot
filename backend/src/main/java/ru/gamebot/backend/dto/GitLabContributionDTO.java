package ru.gamebot.backend.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class GitLabContributionDTO {
    @JsonAlias("target_type")
    private String targetType;
    @JsonAlias("action_name")
    private String actionName;

    public void splitActionName(){
        this.actionName = actionName.split(" ")[0];
    }

}
