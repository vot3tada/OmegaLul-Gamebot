package ru.gamebot.backend.controllers;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.gamebot.backend.dto.GetAllQuizDTO;
import ru.gamebot.backend.dto.QuestionDTO;
import ru.gamebot.backend.dto.QuizDTO;
import ru.gamebot.backend.services.QuizService;
import ru.gamebot.backend.util.exceptions.ErrorResponse;
import ru.gamebot.backend.util.exceptions.QuizExceptions.QuizNotFoundException;

import java.util.List;

@RestController
@RequestMapping("/api/quiz")
@RequiredArgsConstructor
@Slf4j
public class QuizController {

    public final QuizService quizService;

    @GetMapping("/all")
    public List<GetAllQuizDTO> getAllQuiz(){
        return quizService.getAllQuiz();
    }

    @GetMapping("/id/{id}")
    public QuizDTO getQuiz(@PathVariable("id") Integer id){
        return quizService.getQuizById(id);
    }

    @PostMapping("/create")
    public ResponseEntity<GetAllQuizDTO> createQuiz(@RequestBody QuizDTO quizDTO){
        var quiz = quizService.createQuiz(quizDTO);
        return new ResponseEntity<>(quiz, HttpStatus.CREATED);
    }

    @PostMapping("/add/question")
    public ResponseEntity<QuestionDTO> addQuestionToQuiz(@RequestBody QuestionDTO questionDTO){
        var question = quizService.createQuestion(questionDTO);
        return new ResponseEntity<>(question, HttpStatus.CREATED);
    }

    @DeleteMapping("/delete/{id}")
    public ResponseEntity<HttpStatus> deleteQuiz(@PathVariable("id") Integer id){
        quizService.deleteQuiz(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @ExceptionHandler
    public ResponseEntity<ErrorResponse> handleException(QuizNotFoundException e){
        var response = new ErrorResponse("Quiz not found!");
        return new ResponseEntity<>(response,HttpStatus.NOT_FOUND);
    }
}
