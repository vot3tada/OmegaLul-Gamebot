package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
public class GetGitlabDTO {
    private Integer userId;
    List<Contribution> contributions;
    @Data
    public static class Contribution{
        private String action;
        private Integer count;

        public Contribution(String action, Integer count) {
            this.action = action;
            this.count = count;
        }
    }

    public GetGitlabDTO(Integer userId, List<Contribution> contributions) {
        this.userId = userId;
        this.contributions = contributions;
    }
}
