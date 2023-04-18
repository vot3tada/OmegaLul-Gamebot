package ru.gamebot.backend.services;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import ru.gamebot.backend.dto.GetAllQuizDTO;
import ru.gamebot.backend.dto.QuestionDTO;
import ru.gamebot.backend.dto.QuizDTO;
import ru.gamebot.backend.repository.QuestionRepository;
import ru.gamebot.backend.repository.QuizRepository;
import ru.gamebot.backend.util.exceptions.QuizExceptions.QuizNotFoundException;
import ru.gamebot.backend.util.mappers.QuizMapper.QuestionMapper;
import ru.gamebot.backend.util.mappers.QuizMapper.QuizMapper;

import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class QuizService {
    private final QuizRepository quizRepository;
    private final QuizMapper quizMapper;
    private final QuestionRepository questionRepository;
    private final QuestionMapper questionMapper;

    public QuizDTO getQuizById(Integer id){
        var quiz = quizRepository.findById(id).orElseThrow(QuizNotFoundException::new);
        return quizMapper.quizToQuizDTO(quiz);
    }

    public List<GetAllQuizDTO> getAllQuiz(){
        var quizzes = quizRepository.findAll();
        return quizzes.stream().map(quizMapper::quizToAllQuizDTO).toList();
    }

    @Transactional
    public GetAllQuizDTO createQuiz(QuizDTO quizDTO) {
        var quiz = quizMapper.quizDTOToQuiz(quizDTO);
        return quizMapper.quizToAllQuizDTO(quizRepository.save(quiz));
    }

    @Transactional
    public QuestionDTO createQuestion(QuestionDTO questionDTO){
        var quiz = quizRepository.findById(questionDTO.getQuizId()).orElseThrow(QuizNotFoundException::new);
        var question = questionMapper.questionDTOToQuestion(questionDTO);
        question.setQuiz(quiz);
        var saveQuestion = questionRepository.save(question);
        questionDTO.setId(saveQuestion.getId());
        return questionDTO;
    }

    @Transactional
    public void deleteQuiz(Integer id){
        quizRepository.delete(quizRepository.findById(id)
                            .orElseThrow(QuizNotFoundException::new));
    }
}
