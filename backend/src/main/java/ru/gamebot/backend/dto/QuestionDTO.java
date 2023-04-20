package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class QuestionDTO {
    private Integer id;
    private String text;
    private String answer;
    private String photo;
    private Integer quizId;
}
