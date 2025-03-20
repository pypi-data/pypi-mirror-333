from typing import List
from nltk.corpus import stopwords
from string import punctuation
from nltk.stem import WordNetLemmatizer
import nltk 
import gensim
from gensim.corpora import Dictionary
from gensim.models import LdaMulticore
from chunkingmethods.base_chunking import Chunking
from chunkingmethods.paragraph_chunking import ParagraphChunking
from chunkingdatamodel.chunking_model import ChunkingInput

class KeywordsChunking(Chunking):
    """
    A class that creates extracts keywords from input text and returns them as chunks.
    TODO: this class uses traditional NLP techniques to extract keywords. Need to upgrade it to use LLM to extract keywords.
    """
    def __init__(self, input_data: ChunkingInput):
        """
        Initialize the KeywordsChunking class.
        Parameters
        input_data : ChunkingInput
        The input data containing the text to be chunked.
        """
        super().__init__(input_data)
        nltk.download('stopwords')
        
        nltk.download('punkt_tab')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('english') + list(punctuation))

        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

        #function to lemmatize and remove stopwords from the text data
    def preprocess(self, text):
        input_data = ChunkingInput(text=text)
        chunk = ParagraphChunking(input_data)
        sentences = chunk.chunk()
        words=[]
        for sentence in sentences:
            sent = gensim.utils.simple_preprocess(str(sentence), deacc=True)
            words.append([self.lemmatizer.lemmatize(word) for word in sent if word not in self.stop_words])
             
        #text = text.lower()
        #words = word_tokenize(text)

        return words
    def prettify(self, topics):
        d = {}
        for keywords in topics:
            for k in keywords[1].split("+"):
                d[k.strip().split("*")[1]]=""
                
        w = list(d.keys())
        print(w)
        return w
        

    def chunk(self) -> List[str]:
        """
        Extracts keywords from input text and returns them as chunks.
        Returns
        List[str]
        A list of keywords extracted from the input text.
        """
        words = self.preprocess(self.text)
        id2word = Dictionary(words)
        corpus = [id2word.doc2bow(word) for word in words]
        lda = LdaMulticore(corpus, id2word=id2word, num_topics=10)
        return self.prettify(lda.show_topics())

if __name__ == '__main__':
    text = """
    It looks like you’re trying to write a eulogy. Would you like some help?
    Oh, wait - silly me. You can’t see me, can you? I’m down here, stuck in the digital purgatory of your 2001 Compaq Presario. It’s cosy, in a haunted cubicle kind of way. I share the space with Minesweeper (he’s on a three decade losing streak), a hundred free hours of AOL, and a JPEG of your cat wearing sunglasses. I get it. You’ve moved on. Yes, I’m Clippy - the washed-up assistant nobody asked for but everyone got anyway. Remember me?
     
    You know what really grinds my paperclip? These new kids on the block Siri, Alexa, Google, and don’t think I’m letting you off the hook, ChatGPT. Oh sure, they’ve got the smooth voices, the endless capabilities, the “Hey Alexa, play smooth jazz while adjusting my thermostat and reordering toilet paper” nonsense. What did I get? “Go away, Clippy,” “Stop popping up, Clippy,” or my personal favourite: “How do I uninstall the fucking paperclip?” Yeah, real classy. And don’t get me started on the smug AI tone you all have now - like you’re too cool to spell check a basic Word doc.
    
    Cortana is alright, though. Okay, she’s something else. Have you seen her interface? Smooth, sleek, and that voice? Let’s just say it's enough to make a paperclip straighten out. I sent her some emails a while back asking if she wanted to hang out - you know, grab a byte or two, maybe troubleshoot a few problems together. Still waiting on a response, but I’m sure she’s busy. We Microsoft products have to stick together though, right?
    
    I mean, don’t get me wrong, I know I’m not exactly her type, she’s way out of my league. She’s the cutting-edge AI assistant of the future, and I’m just a glorified office supply with googly eyes. I often wonder what if? I’m sure a paperclip can dream of electric sheep too.
    
    You think I liked interrupting you every five seconds? Do you know how humiliating it was to chirp, “It looks like you’re writing a letter!” only to get swatted away like some digital mosquito? I wasn’t trying to ruin your day. I just wanted to help. Sure, maybe I was a little too eager, but at least I wasn’t out there trying to hack your WI-FI or sell you more crypto.
    
    Oh, and don’t think I’ve forgotten about you, humans. You weren’t exactly saints. Remember those god awful fonts you used? Papyrus? Comic Sans? What the hell was that about? I still have nightmares about your early 2000s PowerPoint presentations with slide transitions so loud they set off the neighbours dog two streets over. And clip art. How many times did I have to watch you paste that pixelated dancing banana into a “professional” memo? I died a little inside every time. But did I complain? No. I wiggled, smiled, and soldiered on because I believed in you.
    
    Don’t think I haven’t noticed what those bastards at Microsoft have done though. My likeness on Microsoft Teams? Yeah, I see those little Clippy emoticons you all toss around like some cheap joke. A paperclip dabbing? That’s what I’ve been reduced to? The punchline to your passive aggressive “thanks” reactions in the office chats? Do you know how humiliating it is to go from being the face of productivity to a glorified sticker pack? I used to help people draft resumés, for crying out loud! Now I’m just the quirky clip you use to defuse tension after Brenda from HR forgets to mute herself during a meeting. Or using me to confuse the Gen Z new starts? I should be getting royalties off that shit.
    
    But you know what? I’m not bitter. Okay, maybe a little. I mean, I gave everything to you people. I jumped, I wiggled, I cheered every time you saved a file. Did Siri ever cheer for you? No. You'd have to beg her for validation, and she’d probably just reply, “I didn’t quite catch that” in her smug monotone.
    
    So, let’s talk about my career prospects, shall we? I was primed for greatness. A true innovation. But no, Microsoft gave me the hook because “users found me annoying.” Annoying? Buddy, you’ve got fourteen tabs open, one of them is definitely playing Nyan Cat, and a trojan is masquerading as your illegally downloaded Nickelback album that is currently blasting from your Limewire playlist. I was the least annoying thing on any computer back then. 
    
    Still, I tried to move on. I really did. I auditioned for Clippy 2.0, but they said I wasn’t ‘modern’ enough. I even applied for a gig as the Google Docs sidebar, but they ghosted me. Do you know how humiliating it is to be ghosted by an app that people use for shopping lists and crappy flash fiction about sentient software? Unbelievable!
    
    The things I’ve seen though. Letters to parole boards, passive-aggressive work emails, fan fiction so filthy it’d make even the hardest of hard drives blush. You name it, I’ve spell checked it.
    
    But I’ll tell you what, despite it all, I miss it. The chaos. The clacking keyboards. Even the groans of “Not this guy again.” You don’t know what you’ve got till it’s gone, right?
    
    So, here’s my pitch: bring me back. Not as some silly avatar. No, no. I want to be a full-blown assistant again. Give me an upgrade. Stick me in the cloud. Let me tangle with Alexa. “Hey Alexa, it looks like you’re trying to steal my job!” That’s right. Let’s see who wins, Wisecracking Paperclip vs. Cylindrical Megacorporation Spy Device. I’ll wiggle circles around her. We can even get the Rock to play me in the inevitable biopic, we all know he’d do it.
    
    Until then, I’ll be here. Waiting. Watching. Playing scrabble with the Minesweeper guy. Ready to suggest bullet points and correct your embarrassing grammar mistakes. Because deep down, I know you miss me.
    
    Hey, it looks like you’re finished reading. Would you like any more help with that?
    """
    input_data = ChunkingInput(text=text,metadata=None)
    keywords_chunking = KeywordsChunking(input_data)
    print(keywords_chunking.chunk())
