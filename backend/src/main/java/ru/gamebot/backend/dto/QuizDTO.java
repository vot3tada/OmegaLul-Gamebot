package ru.gamebot.backend.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
public class QuizDTO {
    private Integer id;
    private String name;
    private String photo;
    private List<QuestionDTO> questions;
}
