import { Test, TestingModule } from '@nestjs/testing';
import { NationsService } from './nations.service';

describe('NationsService', () => {
  let service: NationsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [NationsService],
    }).compile();

    service = module.get<NationsService>(NationsService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
