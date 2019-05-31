package com.example.david.neogame;

import android.content.pm.ActivityInfo;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;

public class MainActivity extends AppCompatActivity {
    Button mMyCardButtons[];
    Button mOpponentCardButtons[];
    Button mMyBoardButtons[];
    Button mOpponentBoardButtons[];
    TextView mTextView;

    int mDeck[];
    int mMyCards[];
    int mOpponentCards[];
    int mMyBoard[];
    int mOpponentBoard[];
    int mMyPick[];
    int mOpponentPick[];

    int mWins;
    int mLosses;

    boolean mGameActive;

    void storeButtons() {
        mMyCardButtons = new Button[5];
        mMyCardButtons[0] = (Button)findViewById(R.id.myCard0);
        mMyCardButtons[1] = (Button)findViewById(R.id.myCard1);
        mMyCardButtons[2] = (Button)findViewById(R.id.myCard2);
        mMyCardButtons[3] = (Button)findViewById(R.id.myCard3);
        mMyCardButtons[4] = (Button)findViewById(R.id.myCard4);

        mOpponentCardButtons = new Button[5];
        mOpponentCardButtons[0] = (Button)findViewById(R.id.opponentCard0);
        mOpponentCardButtons[1] = (Button)findViewById(R.id.opponentCard1);
        mOpponentCardButtons[2] = (Button)findViewById(R.id.opponentCard2);
        mOpponentCardButtons[3] = (Button)findViewById(R.id.opponentCard3);
        mOpponentCardButtons[4] = (Button)findViewById(R.id.opponentCard4);

        mMyBoardButtons = new Button[4];
        mMyBoardButtons[0] = (Button)findViewById(R.id.myBoard0);
        mMyBoardButtons[1] = (Button)findViewById(R.id.myBoard1);
        mMyBoardButtons[2] = (Button)findViewById(R.id.myBoard2);
        mMyBoardButtons[3] = (Button)findViewById(R.id.myBoard3);

        mOpponentBoardButtons = new Button[4];
        mOpponentBoardButtons[0] = (Button)findViewById(R.id.opponentBoard0);
        mOpponentBoardButtons[1] = (Button)findViewById(R.id.opponentBoard1);
        mOpponentBoardButtons[2] = (Button)findViewById(R.id.opponentBoard2);
        mOpponentBoardButtons[3] = (Button)findViewById(R.id.opponentBoard3);
    }

    void createDeck() {
        mDeck = new int[25];
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                mDeck[i * 5 + j] = j;
            }
        }
    }

    void shuffleDeck() {
        Random rnd = new Random();
        for (int i = mDeck.length - 1; i > 0; i--) {
            int index = rnd.nextInt(i + 1);
            // Simple swap
            int a = mDeck[index];
            mDeck[index] = mDeck[i];
            mDeck[i] = a;
        }
    }

    void opponentMoveRnd() {
        mOpponentPick = new int[2];
        Random rnd = new Random();
        int pick0 = rnd.nextInt(5);
        int pick1 = rnd.nextInt(4);
        if (pick1 >= pick0) {
            pick1 += 1;
        }
        mOpponentPick[0] = pick0;
        mOpponentPick[1] = pick1;
    }

    void opponentMoveMax() {
        // Picks the cards that maximize results from
        // the currently shown board
        mOpponentPick = new int[2];
        //Random rnd = new Random();
        int pick0 = 0;
        int pick1 = 1;
        int maxRes = -17;

        for (int i = 0; i < 4; i++) {
            for (int j = i + 1; j < 5; j++) {
                int res = opponentEvaluateBoard(i, j);
                if (res > maxRes) {
                    maxRes = res;
                    pick0 = i;
                    pick1 = j;
                }
            }
        }
        mOpponentPick[0] = pick0;
        mOpponentPick[1] = pick1;
    }

    void newGame() {
        mGameActive = true;
        shuffleDeck();
        // after deck shuffle draw 14 cards
        mMyCards = new int[5];
        mOpponentCards = new int[5];
        for (int i = 0; i < 5; i ++) {
            mMyCards[i] = mDeck[i];
            mOpponentCards[i] = mDeck[i + 5];
        }
        mMyBoard = new int[4];
        mOpponentBoard = new int[4];
        for (int i = 0; i < 2; i ++) {
            mMyBoard[i] = mDeck[i + 10];
            mOpponentBoard[i] = mDeck[i + 12];
            // -1 since they have not been played
            mMyBoard[i + 2] = -1;
            mOpponentBoard[i + 2] = -1;
        }
        mMyPick = new int[2];
        mMyPick[0] = -1;
        mMyPick[1] = -1;
        opponentMoveMax();
    }

    void updateView() {
        mTextView.setText("Wins: " + mWins + ", Losses: " + mLosses);
        if (mMyPick[0] == -1) {
            mMyBoard[2] = -1;
        } else {
            mMyBoard[2] = mMyCards[mMyPick[0]];
        }

        if (mMyPick[1] == -1) {
            mMyBoard[3] = -1;
        } else {
            mMyBoard[3] = mMyCards[mMyPick[1]];
        }

        for (int i = 0; i < 5; i++) {
            // if the card has been marked don't display it
            if (i == mMyPick[0] || i == mMyPick[1]) {
                mMyCardButtons[i].setText("-");
            } else {
                int val = mMyCards[i];
                mMyCardButtons[i].setText(Integer.toString(val));
            }

            if (i == mOpponentPick[0] || i == mOpponentPick[1]) {
                mOpponentCardButtons[i].setText("-");
            } else {
                mOpponentCardButtons[i].setText("");
            }
        }
        for (int i = 0; i < 4; i++) {
            int myVal = mMyBoard[i];
            int opponentVal = mOpponentBoard[i];
            if (myVal == -1) {
                mMyBoardButtons[i].setText("");
            }else {
                mMyBoardButtons[i].setText(Integer.toString(myVal));
            }
            if (opponentVal == -1) {
                mOpponentBoardButtons[i].setText("");
            }else {
                mOpponentBoardButtons[i].setText(Integer.toString(opponentVal));
            }
        }
    }

    void setupButtons() {
        for (int i = 0; i < 5; i++) {
            final int idx = i;
            mMyCardButtons[i].setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    if (!mGameActive) {
                        newGame();
                        updateView();
                        return;
                    }
                    // unmark card if it is marked
                    if (idx == mMyPick[0]) {
                        mMyPick[0] = -1;
                        updateView();
                        return;
                    }
                    if (idx == mMyPick[1]) {
                        mMyPick[1] = -1;
                        updateView();
                        return;
                    }
                    if (mMyPick[0] == -1) {
                        mMyPick[0] = idx;
                    } else {
                        mMyPick[1] = idx;
                        mGameActive = false;
                        evaluate();
                        return;
                    }
                    updateView();

                }
            });
        }
        Button newGameButton = (Button)findViewById(R.id.newGame);
        newGameButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                mWins = 0;
                mLosses = 0;
                newGame();
                updateView();
            }
        });
    }

    int compare(int i1, int i2) {
        int diff = i1 - i2;
        if (diff == 4) {
            return -1;
        }
        if (diff == -4) {
            return 1;
        }
        return 0;
    }

    int getResult(int[] board0, int[] board1) {
        int result = 0;
        for (int i = 0; i < board0.length; i++) {
            for (int j = 0; j < board1.length; j++) {
                result += compare(board0[i], board1[j]);
            }
        }
        return result;
    }

    void evaluate() {
        mOpponentBoard[2] = mOpponentCards[mOpponentPick[0]];
        mOpponentBoard[3] = mOpponentCards[mOpponentPick[1]];
        updateView();
        int result = getResult(mMyBoard, mOpponentBoard);
        if (result > 0) {
            mTextView.setText("You Win! Result: " + result);
            mWins += 1;
            return;
        } else if(result < 0) {
            mTextView.setText("You Loose! Result: " + result);
            mLosses += 1;
            return;
        } else {
            mTextView.setText("Draw!");
        }
    }

    int opponentEvaluateBoard(int pick0, int pick1) {
        int[] opponentBoard = new int[4];
        opponentBoard[0] = mOpponentBoard[0];
        opponentBoard[1] = mOpponentBoard[1];
        opponentBoard[2] = mOpponentCards[pick0];
        opponentBoard[3] = mOpponentCards[pick1];
        return getResult(opponentBoard, mMyBoard);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        setContentView(R.layout.activity_main);
        mTextView = (TextView)findViewById(R.id.textView);
        mWins = 0;
        mLosses = 0;
        storeButtons();
        setupButtons();
        createDeck();
        newGame();
        updateView();
    }

}
